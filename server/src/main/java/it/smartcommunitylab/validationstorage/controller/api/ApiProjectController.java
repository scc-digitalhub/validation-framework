package it.smartcommunitylab.validationstorage.controller.api;

import java.util.List;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseProjectController;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;

@RestController
@RequestMapping(value = "/api/p")
public class ApiProjectController extends BaseProjectController {
    @PreAuthorize("permitAll()")
    @GetMapping
    public List<ProjectDTO> find() {
        return service.findProjects();
    }
}
