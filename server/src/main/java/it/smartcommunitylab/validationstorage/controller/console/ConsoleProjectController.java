package it.smartcommunitylab.validationstorage.controller.console;

import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseProjectController;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;

@RestController
@RequestMapping(value = "/console/p")
public class ConsoleProjectController extends BaseProjectController {
    @PreAuthorize("permitAll()")
    @GetMapping
    public Page<ProjectDTO> find(Pageable pageable, Authentication authentication) {
        Set<String> authorities = authentication.getAuthorities().stream().map(a -> a.getAuthority()).filter(a -> a.startsWith("PROJECT_")).map(a -> a.substring("PROJECT_".length())).collect(Collectors.toSet());
        return service.findProjects(authorities, pageable);
    }
}
