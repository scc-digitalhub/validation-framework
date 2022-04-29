package it.smartcommunitylab.validationstorage.controller.api;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseExperimentController;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment")
public class ApiExperimentController extends BaseExperimentController {
    
    @GetMapping
    public List<ExperimentDTO> find(
            @PathVariable String projectId) {
        return service.findExperiments(projectId);
    }
    
}
