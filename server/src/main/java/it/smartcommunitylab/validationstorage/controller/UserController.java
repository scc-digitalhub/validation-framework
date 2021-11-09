package it.smartcommunitylab.validationstorage.controller;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.InsufficientAuthenticationException;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;

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

    @Valid
    public class UserDTO {
        @NotNull
        private String username;

        public UserDTO(String username) {
            this.username = username;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }
    }
}