package it.smartcommunitylab.validationstorage.controller.console;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseExperimentController;
import it.smartcommunitylab.validationstorage.model.dto.ExperimentDTO;

@RestController
@RequestMapping(value = "/console/p/{projectId}/experiment")
public class ConsoleExperimentController extends BaseExperimentController {
    
    @GetMapping
    public Page<ExperimentDTO> find(
            @PathVariable String projectId,
            Pageable pageable) {
        return service.findExperiments(projectId, pageable);
    }

}
