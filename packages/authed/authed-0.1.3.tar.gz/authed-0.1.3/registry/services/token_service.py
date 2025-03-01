import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from uuid import UUID, uuid4
from jwt import PyJWTError

from .. import models
from ..core.config import get_settings
from ..core.logging.logging import log_service
from ..core.logging.models import LogLevel
from ..core.security.key_manager import KeyManager
from ..core.security.dpop import DPoPVerifier
from ..services.agent_service import AgentService
from ..core.security.encryption import EncryptionManager

# Use RS256 (RSA + SHA-256) instead of HS256 (HMAC + SHA-256)
JWT_ALGORITHM = "RS256"

key_manager = KeyManager()
dpop_verifier = DPoPVerifier()
REGISTRY_PRIVATE_KEY = key_manager.get_private_key()
REGISTRY_PUBLIC_KEY = key_manager.get_public_key()
field_encryption = EncryptionManager()

settings = get_settings()

class TokenService:
    def __init__(self):
        """Initialize the token service."""
        self.settings = get_settings()
        self.dpop_verifier = DPoPVerifier()
        self.agent_service = AgentService()
        self.key_manager = KeyManager()
        self.field_encryption = EncryptionManager()

    def _check_agent_has_permission(self, agent_permissions: List[models.AgentPermission], target_agent_id: str, target_provider_id: str) -> bool:
        """Check if an agent has permission for a target (either directly or via provider)."""
        for perm in agent_permissions:
            if perm.type == models.PermissionType.ALLOW_AGENT and perm.target_id == target_agent_id:
                return True
            if perm.type == models.PermissionType.ALLOW_PROVIDER and perm.target_id == target_provider_id:
                return True
        return False

    def _verify_agent_permissions(self, requesting_agent_id: UUID, target_agent_id: UUID) -> bool:
        """Verify that both agents have permissions to interact with each other."""
        try:
            # Get both agents
            requesting_agent = self.agent_service.get_agent(str(requesting_agent_id))
            target_agent = self.agent_service.get_agent(str(target_agent_id))
            
            if not requesting_agent or not target_agent:
                log_service.log_event(
                    "permission_check_failed",
                    {
                        "error": "One or both agents not found",
                        "requesting_agent": str(requesting_agent_id),
                        "target_agent": str(target_agent_id)
                    },
                    level=LogLevel.ERROR
                )
                return False
            
            # Check if requesting agent has permission for target
            # (either directly or via provider permission)
            requesting_has_permission = self._check_agent_has_permission(
                requesting_agent.permissions,
                str(target_agent_id),
                str(target_agent.provider_id)
            )
            
            # Check if target agent has permission for requester
            # (either directly or via provider permission)
            target_has_permission = self._check_agent_has_permission(
                target_agent.permissions,
                str(requesting_agent_id),
                str(requesting_agent.provider_id)
            )
            
            # Log the permission check
            log_service.log_event(
                "permission_check",
                {
                    "requesting_agent": str(requesting_agent_id),
                    "requesting_provider": str(requesting_agent.provider_id),
                    "target_agent": str(target_agent_id),
                    "target_provider": str(target_agent.provider_id),
                    "requesting_has_permission": requesting_has_permission,
                    "target_has_permission": target_has_permission
                }
            )
            
            # Both agents must have permissions for each other
            return requesting_has_permission and target_has_permission
            
        except Exception as e:
            log_service.log_event(
                "permission_check_error",
                {
                    "error": str(e),
                    "requesting_agent": str(requesting_agent_id),
                    "target_agent": str(target_agent_id)
                },
                level=LogLevel.ERROR
            )
            return False

    def create_interaction_token(
        self,
        agent_id: UUID,
        target_agent_id: UUID,
        dpop_proof: str,
        dpop_public_key: str,
        method: str,
        url: str,
        expires_delta: Optional[timedelta] = None
    ) -> models.InteractionToken:
        """Create a new interaction token
        
        Args:
            agent_id: The ID of the requesting agent
            target_agent_id: The ID of the target agent this token is valid for
            dpop_proof: The DPoP proof for this request
            dpop_public_key: The agent's DPoP public key
            method: The HTTP method used
            url: The request URL
            expires_delta: Optional custom expiration time
        """
        try:
            # First verify that both agents have permissions for each other
            if not self._verify_agent_permissions(agent_id, target_agent_id):
                raise ValueError(
                    f"Insufficient permissions between agents {agent_id} and {target_agent_id}"
                )
            
            # Then verify the DPoP proof
            if not self.dpop_verifier.verify_proof(dpop_proof, dpop_public_key, method, url):
                raise ValueError("Invalid DPoP proof")
            
            if expires_delta is None:
                expires_delta = timedelta(minutes=self.settings.TOKEN_EXPIRY_MINUTES)
            
            now = datetime.now(timezone.utc)
            expires_at = now + expires_delta
            token_id = str(uuid4())
            
            # Calculate proof hash for binding
            dpop_hash = self.dpop_verifier.hash_dpop_proof(dpop_proof)
            
            # Encrypt sensitive data
            encrypted_dpop_key = self.key_manager.encrypt_data(dpop_public_key)
            
            to_encode = {
                "sub": str(agent_id),
                "target": str(target_agent_id),
                "dpop_hash": dpop_hash,
                "dpop_public_key": encrypted_dpop_key,
                "exp": int(expires_at.timestamp()),
                "iat": int(now.timestamp()),
                "iss": "registry",
                "jti": token_id,
                "nbf": int(now.timestamp()),
                "typ": "interaction_token"
            }
            
            encoded_jwt = jwt.encode(
                to_encode, 
                REGISTRY_PRIVATE_KEY,
                algorithm=JWT_ALGORITHM
            )
            
            log_service.log_event("token_issued", {
                "token_id": token_id,
                "agent_id": str(agent_id),
                "target_agent_id": str(target_agent_id),
                "expires_at": expires_at.isoformat()
            }, level=LogLevel.INFO)
            
            return models.InteractionToken(
                token=encoded_jwt,
                target_agent_id=target_agent_id,
                expires_at=expires_at
            )
            
        except Exception as e:
            log_service.log_event(
                "token_creation_error",
                {
                    "error": str(e),
                    "agent_id": str(agent_id),
                    "target_agent_id": str(target_agent_id)
                },
                level=LogLevel.ERROR
            )
            raise ValueError(f"Failed to create token: {str(e)}")

    def verify_token(
        self,
        token: str,
        expected_target: Optional[UUID] = None,
        dpop_proof: Optional[str] = None,
        method: Optional[str] = None,
        url: Optional[str] = None
    ) -> dict:
        """Verify an interaction token.
        
        Args:
            token: The interaction token to verify
            expected_target: Optional target agent ID to verify against
            dpop_proof: DPoP proof from the verifying agent
            method: HTTP method of the verification request
            url: URL of the verification request
            
        Returns:
            dict: The decoded token payload
            
        Raises:
            ValueError: If token is invalid or verification fails
        """
        try:
            # Decode and verify the token using the registry's public key
            payload = jwt.decode(
                token,
                REGISTRY_PUBLIC_KEY,  # Use the global public key that matches the private key used for signing
                algorithms=["RS256"]
            )
            
            # Verify target if provided
            if expected_target and str(expected_target) != payload["target"]:
                raise ValueError("Target agent ID mismatch")
                
            # Verify DPoP proof from verifying agent
            if dpop_proof and method and url:
                # Get verifying agent
                verifying_agent = self.agent_service.get_agent(payload["target"])
                if not verifying_agent:
                    raise ValueError("Verifying agent not found")
                    
                # Decrypt the verifying agent's public key using field encryption
                try:
                    decrypted_public_key = self.field_encryption.decrypt_field(verifying_agent.dpop_public_key)
                except ValueError as e:
                    log_service.log_event(
                        "dpop_verification_error",
                        {"error": f"Failed to decrypt verifying agent's public key: {str(e)}"},
                        level=LogLevel.ERROR
                    )
                    raise ValueError("Failed to decrypt verifying agent's public key")

                # Ensure proper PEM format
                if not decrypted_public_key.startswith('-----BEGIN PUBLIC KEY-----'):
                    decrypted_public_key = f"-----BEGIN PUBLIC KEY-----\n{decrypted_public_key}\n-----END PUBLIC KEY-----"

                # Verify the new DPoP proof
                if not self.dpop_verifier.verify_proof(
                    dpop_proof,
                    decrypted_public_key,
                    method,
                    url
                ):
                    raise ValueError("Invalid DPoP proof from verifying agent")
                    
            # Verify permissions are still valid
            if not self._verify_agent_permissions(
                UUID(payload["sub"]),
                UUID(payload["target"])
            ):
                raise ValueError("Agent permissions have been revoked")
                
            return payload
            
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise ValueError(f"Token verification failed: {str(e)}") 