package it.smartcommunitylab.validationstorage.auth;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.authentication.configurers.provisioning.InMemoryUserDetailsManagerConfigurer;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import it.smartcommunitylab.validationstorage.config.AuthenticationProperties;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class CustomWebSecurityConfigurerAdapter extends WebSecurityConfigurerAdapter {
	
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
		switch (authenticationProperties.getType().toLowerCase()) {
		
			case "basic":
				http.cors().and().csrf().disable()
					.authorizeRequests()
					.anyRequest()
					.authenticated()
					.and()
					.httpBasic();
				
				break;
				
			case "oauth2":
				
			default:
				http.cors().and().csrf().disable()
					.authorizeRequests()
					.anyRequest()
					.permitAll();
				break;
				
		}
	}
	
	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
}