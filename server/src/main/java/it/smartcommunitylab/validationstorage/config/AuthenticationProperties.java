package it.smartcommunitylab.validationstorage.config;

import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import lombok.Data;

@Data
@Component
@ConfigurationProperties(prefix = "auth")
public class AuthenticationProperties {
    private String type;
	
	private String projectAuthorityPrefix;
	
    private List<User> users;
    
    @Data
    public static class User {
    	private String username;
    	private String password;
    	private List<String> authorities;
    }
}