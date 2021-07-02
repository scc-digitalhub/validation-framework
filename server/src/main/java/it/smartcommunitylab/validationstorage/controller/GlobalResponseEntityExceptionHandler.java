package it.smartcommunitylab.validationstorage.controller;

import java.time.Instant;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.ServletWebRequest;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;

@ControllerAdvice
public class GlobalResponseEntityExceptionHandler extends ResponseEntityExceptionHandler {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS+00:00").withZone(ZoneOffset.UTC);

    /**
     * Builds a ResponseEntity with a detailed body.
     * 
     * @param ex      Exception.
     * @param status  HTTP status.
     * @param request Web request.
     * @return ResponseEntity with a detailed body.
     */
    private ResponseEntity<Object> buildResponse(RuntimeException ex, HttpStatus status, WebRequest request) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("timestamp", formatter.format(Instant.now()));
        body.put("status", status.value());
        body.put("error", status.getReasonPhrase());
        body.put("message", ex.getMessage());

        if (request instanceof ServletWebRequest)
            body.put("path", ((ServletWebRequest) request).getRequest().getRequestURI());

        return handleExceptionInternal(ex, body, new HttpHeaders(), status, request);
    }

    @ExceptionHandler(value = { IllegalArgumentException.class })
    protected ResponseEntity<Object> handleIllegalArgument(IllegalArgumentException ex, WebRequest request) {
        return buildResponse(ex, HttpStatus.BAD_REQUEST, request);
    }

    @ExceptionHandler(value = { DocumentAlreadyExistsException.class })
    protected ResponseEntity<Object> handleDocumentAlreadyExists(DocumentAlreadyExistsException ex, WebRequest request) {
        return buildResponse(ex, HttpStatus.CONFLICT, request);
    }

    @ExceptionHandler(value = { DocumentNotFoundException.class })
    protected ResponseEntity<Object> handleDocumentNotFound(DocumentNotFoundException ex, WebRequest request) {
        return buildResponse(ex, HttpStatus.NOT_FOUND, request);
    }

    @ExceptionHandler(value = { AccessDeniedException.class })
    protected ResponseEntity<Object> handleAccessDenied(AccessDeniedException ex, WebRequest request) {
        return buildResponse(ex, HttpStatus.FORBIDDEN, request);
    }
}
