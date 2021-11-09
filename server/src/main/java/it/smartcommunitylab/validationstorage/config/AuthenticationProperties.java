package it.smartcommunitylab.validationstorage.config;

import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * Contains various configurations related to authentication.
 */
@Component
@ConfigurationProperties(prefix = "auth")
public class AuthenticationProperties {
    private boolean enabled;

    private String projectAuthorityPrefix;
    private String aacClaim;
    private String aacClaimProjects;

    private List<User> users;
    
    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getProjectAuthorityPrefix() {
        return projectAuthorityPrefix;
    }

    public void setProjectAuthorityPrefix(String projectAuthorityPrefix) {
        this.projectAuthorityPrefix = projectAuthorityPrefix;
    }

    public String getAacClaim() {
        return aacClaim;
    }

    public void setAacClaim(String aacClaim) {
        this.aacClaim = aacClaim;
    }

    public String getAacClaimProjects() {
        return aacClaimProjects;
    }

    public void setAacClaimProjects(String aacClaimProjects) {
        this.aacClaimProjects = aacClaimProjects;
    }

    public List<User> getUsers() {
        return users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }

    public static class User {
        private String username;
        private String password;
        private List<String> authorities;

        public String getUsername() {
            return username;
        }
        
        public void setUsername(String username) {
            this.username = username;
        }
        
        public String getPassword() {
            return password;
        }
        
        public void setPassword(String password) {
            this.password = password;
        }
        
        public List<String> getAuthorities() {
            return authorities;
        }
        
        public void setAuthorities(List<String> authorities) {
            this.authorities = authorities;
        }
    }
}