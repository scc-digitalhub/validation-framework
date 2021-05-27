package it.smartcommunitylab.validationstorage.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.authentication.configurers.provisioning.InMemoryUserDetailsManagerConfigurer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Adapter for UI end-points, also works as default adapter.
 */
@Configuration
@Order(10)
public class UiConfigurerAdapter extends WebSecurityConfigurerAdapter {
	
	/**
	 * Contains various configurations for authentication.
	 */
	@Autowired
	private AuthenticationProperties authenticationProperties;
	
	@Autowired
	private PasswordEncoder encoder;
	
	@Autowired
	public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
		InMemoryUserDetailsManagerConfigurer<AuthenticationManagerBuilder> configurer = auth.inMemoryAuthentication();
		
		for (AuthenticationProperties.User user : authenticationProperties.getUsers()) {
			configurer.withUser(user.getUsername())
					.password(encoder.encode(user.getPassword()))
					.authorities(user.getAuthorities().toArray(new String[0]));
		}
	}
	
	@Override
	protected void configure(HttpSecurity http) throws Exception {
		if (authenticationProperties.isEnabled()) {
			http.cors().and().csrf().disable()
				.authorizeRequests()
				.anyRequest()
				.authenticated()
				.and()
				.httpBasic();
		} else {
			http.cors().and().csrf().disable()
			.authorizeRequests()
			.anyRequest()
			.permitAll();
		}
	}
	
	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
}