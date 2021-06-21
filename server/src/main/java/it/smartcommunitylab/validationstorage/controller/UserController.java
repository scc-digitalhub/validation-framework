package it.smartcommunitylab.validationstorage.controller;

import java.security.Principal;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
	@GetMapping("/user")
	public ResponseEntity<Principal> getUser(Principal principal) {
		return ResponseEntity.ok(principal);
	}
}