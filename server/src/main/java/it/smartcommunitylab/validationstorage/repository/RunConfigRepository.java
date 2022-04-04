package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.RunConfig;

public interface RunConfigRepository extends CrudRepository<RunConfig, String> {
    List<RunConfig> findByProjectIdAndExperimentId(String projectId, String experimentId);
}
