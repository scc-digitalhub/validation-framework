package it.smartcommunitylab.validationstorage.common;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class DocumentNotFoundException extends RuntimeException {

	/**
	 * Auto-generated ID.
	 */
	private static final long serialVersionUID = 2777285904953466430L;
	
	public DocumentNotFoundException(String message) {
		super(message);
	}
}