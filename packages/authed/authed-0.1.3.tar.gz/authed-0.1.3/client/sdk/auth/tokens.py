"""Token management for agent authentication."""

from typing import Dict, Union, Optional
from datetime import datetime, timezone
import httpx
from uuid import UUID
import json
from urllib.parse import urlparse, parse_qs, urlencode

from ..models import TokenRequest, InteractionToken
from ..exceptions import AuthenticationError, RegistryError

def normalize_url(url: str) -> str:
    """Normalize URL for comparison"""
    parsed = urlparse(url)
    # Sort query parameters
    if parsed.query:
        params = parse_qs(parsed.query)
        sorted_params = {k: sorted(v) for k, v in params.items()}
        query = urlencode(sorted_params, doseq=True)
    else:
        query = ""
    # Normalize port
    port = f":{parsed.port}" if parsed.port and parsed.port not in (80, 443) else ""
    # Always use HTTPS for registry URLs
    scheme = "https" if "getauthed.dev" in parsed.netloc else parsed.scheme
    return f"{scheme}://{parsed.netloc}{port}{parsed.path}"

class UUIDEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts UUID objects to strings."""
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

class TokenManager:
    """Manages authentication tokens for agents."""
    
    def __init__(self, registry_url: str):
        """Initialize the token manager.
        
        Args:
            registry_url: Base URL of the registry service
        """
        self.registry_url = registry_url.rstrip('/')
        # Ensure HTTPS for registry URL
        if self.registry_url.startswith("http://"):
            self.registry_url = "https://" + self.registry_url[7:]
        self._token_cache: Dict[str, InteractionToken] = {}
        
    def _get_cache_key(self, agent_id: str, target_agent_id: Union[str, UUID]) -> str:
        """Generate a cache key for a token."""
        target_id = str(target_agent_id) if isinstance(target_agent_id, UUID) else target_agent_id
        return f"{agent_id}:{target_id}"
        
    def is_token_valid(self, agent_id: str, target_agent_id: Union[str, UUID]) -> bool:
        """Check if a cached token exists and is still valid.
        
        Args:
            agent_id: The requesting agent's ID
            target_agent_id: The target agent's ID
            
        Returns:
            bool: True if a valid token exists in cache
        """
        cache_key = self._get_cache_key(agent_id, target_agent_id)
        if cache_key not in self._token_cache:
            return False
            
        token = self._token_cache[cache_key]
        now = datetime.now(timezone.utc)
        
        # Check if token has expired
        if token.expires_at <= now:
            del self._token_cache[cache_key]
            return False
            
        return True
        
    async def get_token(
        self,
        agent_id: str,
        agent_secret: str,
        target_agent_id: Union[str, UUID],
        dpop_proof: str,
        dpop_public_key: str,
        registry_url: Optional[str] = None
    ) -> str:
        """Get an authentication token from the registry.
        
        Args:
            agent_id: The agent's ID
            agent_secret: The agent's secret
            target_agent_id: The target agent's ID (can be string or UUID)
            dpop_proof: DPoP proof for the token request
            dpop_public_key: The agent's DPoP public key (PEM format)
            registry_url: Optional override for registry URL (to match request scheme)
            
        Returns:
            str: The authentication token
            
        Raises:
            AuthenticationError: If authentication fails
            RegistryError: If the registry returns an error
        """
        cache_key = self._get_cache_key(agent_id, target_agent_id)
        
        # Check cache first
        if self.is_token_valid(agent_id, target_agent_id):
            return self._token_cache[cache_key].token
            
        # Ensure target_agent_id is a string
        if isinstance(target_agent_id, UUID):
            target_agent_id = str(target_agent_id)
            
        # Create token request
        token_request = TokenRequest(
            target_agent_id=target_agent_id,
            dpop_proof=dpop_proof
        )
        
        # Format public key for HTTP header by removing PEM headers and newlines
        formatted_public_key = dpop_public_key
        if "-----BEGIN PUBLIC KEY-----" in formatted_public_key:
            formatted_public_key = formatted_public_key.replace("-----BEGIN PUBLIC KEY-----", "")
            formatted_public_key = formatted_public_key.replace("-----END PUBLIC KEY-----", "")
            formatted_public_key = formatted_public_key.strip()
        formatted_public_key = formatted_public_key.replace("\n", "")
        
        # Set up headers with all required authentication
        headers = {
            "agent-id": agent_id,
            "agent-secret": agent_secret,
            "dpop-public-key": formatted_public_key,
            "dpop": dpop_proof,
            "Content-Type": "application/json"
        }
        
        try:
            # Configure client to enforce HTTPS for registry URLs
            transport = httpx.AsyncHTTPTransport(
                verify=True,
                retries=1
            )
            
            # Ensure HTTPS for registry URLs
            if "getauthed.dev" in self.registry_url:
                base_url = self.registry_url.replace("http://", "https://")
            else:
                base_url = self.registry_url
            
            async with httpx.AsyncClient(
                transport=transport,
                follow_redirects=False,
                base_url=base_url
            ) as client:
                # Convert the request data to JSON using the custom encoder
                request_data = json.loads(
                    json.dumps(token_request.model_dump(), cls=UUIDEncoder)
                )
                
                # Use relative URL path since base_url is set
                response = await client.post(
                    "/tokens/create",
                    headers=headers,
                    json=request_data
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Invalid agent credentials")
                elif response.status_code != 200:
                    raise RegistryError(
                        status_code=response.status_code,
                        detail=response.text
                    )
                    
                # Parse the response into an InteractionToken
                token_data = response.json()
                token = InteractionToken(
                    token=token_data["token"],
                    target_agent_id=token_data["target_agent_id"],  # Will be converted by the model
                    expires_at=datetime.fromisoformat(token_data["expires_at"])
                )
                
                # Cache the token
                self._token_cache[cache_key] = token
                
                return token.token
                
        except httpx.RequestError as e:
            raise RegistryError(
                status_code=500,
                detail=f"Failed to connect to registry: {str(e)}"
            ) 