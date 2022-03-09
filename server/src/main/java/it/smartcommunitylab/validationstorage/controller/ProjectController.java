package it.smartcommunitylab.validationstorage.controller;

import java.util.List;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.dto.ProjectDTO;
import it.smartcommunitylab.validationstorage.service.ProjectService;

@RestController
@RequestMapping(value = "/api/p")
@PreAuthorize(ValidationStorageConstants.PREAUTH_ID)
public class ProjectController {
    @Autowired
    private ProjectService service;
    
    @PreAuthorize(ValidationStorageConstants.PREAUTH_REQUEST_ID)
    @PostMapping
    public ProjectDTO create(@RequestBody @Valid ProjectDTO request) {
        return service.createProject(request);
    }
    
    @PreAuthorize("permitAll()")
    @GetMapping
    public List<ProjectDTO> find() {
        return service.findProjects();
    }

    @GetMapping("/{id}")
    public ProjectDTO findById(@PathVariable String id) {
        return service.findProjectById(id);
    }

    @PutMapping("/{id}")
    public ProjectDTO update(@PathVariable String id, @RequestBody @Valid ProjectDTO request) {
        return service.updateProject(id, request);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable String id) {
        service.deleteProject(id);
    }
}
