package it.smartcommunitylab.validationstorage.config;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

/**
 * Adapter for end-points not meant for the UI.
 */
@Configuration
@Order(5)
public class ApiConfigurerAdapter extends WebSecurityConfigurerAdapter {

    /**
     * Contains various configurations for authentication.
     */
    @Autowired
    private AuthenticationProperties authenticationProperties;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        if (authenticationProperties.isEnabled()) {
            http.cors().and().csrf().disable()
                    .requestMatcher(getRequestMatcher())
                    .authorizeRequests()
                    .anyRequest()
                    .authenticated()
                    .and()
                    .httpBasic()
                    .and()
                    .requestCache((requestCache) -> requestCache.disable())
                    .oauth2ResourceServer()
                    .jwt()
                    .jwtAuthenticationConverter(jwtAuthenticationConverter());
        } else {
            http.cors().and().csrf().disable()
                    .requestMatcher(getRequestMatcher())
                    .authorizeRequests()
                    .anyRequest()
                    .permitAll()
                    .and()
                    .requestCache((requestCache) -> requestCache.disable());
        }

        http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }

    /**
     * Get matcher for the end-points not meant for the UI.
     * 
     * @return
     */
    private RequestMatcher getRequestMatcher() {
        return new AntPathRequestMatcher("/api/**");
    }

    /**
     * Get JWT converter for OAuth2.
     * 
     * @return
     */
    @Bean
    public Converter<Jwt, AbstractAuthenticationToken> jwtAuthenticationConverter() {
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(new Converter<Jwt, Collection<GrantedAuthority>>() {
            @Override
            public Collection<GrantedAuthority> convert(Jwt source) {
                if (source == null)
                    return null;

                Map<String, Object> validationMap = source.getClaimAsMap(authenticationProperties.getAacClaim());
                if (validationMap == null)
                    return null;

                if (validationMap.get(authenticationProperties.getAacClaimProjects()) instanceof List<?>) {
                    List<?> projects = (List<?>) validationMap.get(authenticationProperties.getAacClaimProjects());
                    if (projects != null)
                        return projects.stream()
                                .map(p -> new SimpleGrantedAuthority(
                                        authenticationProperties.getProjectAuthorityPrefix() + p))
                                .collect(Collectors.toList());
                    return null;
                } else
                    return null;
            }

        });
        return converter;
    }

}
