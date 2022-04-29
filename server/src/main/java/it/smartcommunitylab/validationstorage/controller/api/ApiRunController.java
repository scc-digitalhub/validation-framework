package it.smartcommunitylab.validationstorage.controller.api;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseRunController;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;

@RestController
@RequestMapping(value = "/api/p/{projectId}/experiment/{experimentName}/run")
public class ApiRunController extends BaseRunController {
    
    @GetMapping
    public List<RunDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentName) {
        return service.findRuns(projectId, experimentName);
    }
    
}
