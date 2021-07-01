package it.smartcommunitylab.validationstorage.config;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.authentication.configurers.provisioning.InMemoryUserDetailsManagerConfigurer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.authority.mapping.GrantedAuthoritiesMapper;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.core.user.OAuth2UserAuthority;
import org.springframework.security.oauth2.jwt.Jwt;

/**
 * Adapter for UI end-points, also works as default adapter.
 */
@Configuration
@Order(10)
public class UiConfigurerAdapter extends WebSecurityConfigurerAdapter {
	
	@Value("${auth.aac-claim}")
	private String aacClaim;
	
	@Value("${auth.aac-claim-projects}")
	private String aacClaimProjects;

	/**
	 * Contains various configurations for authentication.
	 */
	@Autowired
	private AuthenticationProperties authenticationProperties;

	@Autowired
	private PasswordEncoder passwordEncoder;

	@Autowired
	public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
		InMemoryUserDetailsManagerConfigurer<AuthenticationManagerBuilder> configurer = auth.inMemoryAuthentication();

		for (AuthenticationProperties.User user : authenticationProperties.getUsers()) {
			configurer.withUser(user.getUsername()).password(passwordEncoder.encode(user.getPassword()))
					.authorities(user.getAuthorities().toArray(new String[0]));
		}
	}

	@Override
	protected void configure(HttpSecurity http) throws Exception {
		if (authenticationProperties.isEnabled()) {
			http.authorizeRequests()
					.antMatchers("/user").permitAll()
					.antMatchers("/static/**").permitAll()
					.anyRequest().authenticated().and().oauth2Login()
					.and().cors().and().csrf().disable();
		} else {
			http.cors().and().csrf().disable().authorizeRequests().anyRequest().permitAll();
		}
	}

	@Bean
	public GrantedAuthoritiesMapper userAuthoritiesMapper() {
		return (authorities) -> {
			Set<GrantedAuthority> mappedAuthorities = new HashSet<>();
			
			authorities.forEach(authority -> {
				if (authority.getAuthority().equals("ROLE_USER")) {
					mappedAuthorities.add(authority);
				}
				
				if (OAuth2UserAuthority.class.isInstance(authority)) {
					OAuth2UserAuthority oauth2UserAuthority = (OAuth2UserAuthority) authority;
					Map<String, Object> userAttributes = oauth2UserAuthority.getAttributes();
					
					if (userAttributes.containsKey(aacClaim) && userAttributes.get(aacClaim) instanceof Map<?, ?>) {
						Map<?, ?> validation = (Map<?, ?>) userAttributes.get(aacClaim);
						if (validation.containsKey(aacClaimProjects) && validation.get(aacClaimProjects) instanceof List<?>) {
							List<?> projects = (List<?>) validation.get(aacClaimProjects);
							projects.forEach(p -> mappedAuthorities.add(new SimpleGrantedAuthority(
									authenticationProperties.getProjectAuthorityPrefix() + p)));
						}
					}
				}
			    
			});
			
			return mappedAuthorities;
		};
	}

	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
}