package it.smartcommunitylab.validationstorage.controller.console;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.controller.BaseRunController;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;

@RestController
@RequestMapping(value = "/console/p/{projectId}/experiment/{experimentName}/run")
public class ConsoleRunController extends BaseRunController {
    
    @GetMapping
    public Page<RunDTO> find(
            @PathVariable String projectId,
            @PathVariable String experimentName,
            Pageable pageable) {
        return service.findRuns(projectId, experimentName, pageable);
    }

}
