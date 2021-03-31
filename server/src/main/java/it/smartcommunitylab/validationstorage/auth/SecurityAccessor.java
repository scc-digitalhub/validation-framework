package it.smartcommunitylab.validationstorage.auth;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.InsufficientAuthenticationException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

import it.smartcommunitylab.validationstorage.config.AuthenticationProperties;

@Component
public class SecurityAccessor {
	@Autowired
	private AuthenticationProperties authenticationProperties;
	
	public void checkUserHasPermissions(String projectId) {
		boolean allowed = false;
		
		switch(authenticationProperties.getType().toLowerCase()) {
		
			case "basic":
				Authentication auth = SecurityContextHolder.getContext().getAuthentication();
				if (auth != null && auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals(authenticationProperties.getProjectAuthorityPrefix() + projectId)))
					allowed = true;
				break;
				
			case "oauth2":
				
			default:
				allowed = true;
				
		}
		
		if (!allowed)
			throw new InsufficientAuthenticationException("User is not allowed to perform this operation on project" + projectId + ".");
	}
}
