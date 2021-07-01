package it.smartcommunitylab.validationstorage.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.InsufficientAuthenticationException;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;

import lombok.Data;
import lombok.NonNull;

@RestController
public class UserController {
	@GetMapping("/user")
	public ResponseEntity<UserDTO> getUser(Authentication authentication) {
		if (authentication == null)
			throw new InsufficientAuthenticationException("Missing authentication.");
		
		return ResponseEntity.ok(new UserDTO(authentication.getName()));
	}
	
	@ExceptionHandler(value = { InsufficientAuthenticationException.class })
	protected ResponseEntity<Void> handleAccessDenied(InsufficientAuthenticationException ex, WebRequest request) {
		return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
	}
	
	@Data
	public class UserDTO {
		@NonNull
		private String username;
	}
}