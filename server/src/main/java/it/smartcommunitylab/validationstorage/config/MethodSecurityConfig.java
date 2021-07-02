package it.smartcommunitylab.validationstorage.config;

import org.aopalliance.intercept.MethodInterceptor;
import org.springframework.aop.interceptor.SimpleTraceInterceptor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.access.method.MethodSecurityMetadataSource;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.method.configuration.GlobalMethodSecurityConfiguration;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

/**
 * This class is used to override the methodSecurityInterceptor method, to bypass
 * PreAuthorize and similar annotations when auth is disabled.
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class MethodSecurityConfig extends GlobalMethodSecurityConfiguration {

    @Value("${auth.enabled}")
    private boolean authEnabled;

    /**
     * Overriding this method allows the application to bypass PreAuthorize and similar annotations when auth is disabled.
     */
    public MethodInterceptor methodSecurityInterceptor(MethodSecurityMetadataSource methodSecurityMetadataSource) {
        return authEnabled ? super.methodSecurityInterceptor(methodSecurityMetadataSource) : new SimpleTraceInterceptor();
    }

}