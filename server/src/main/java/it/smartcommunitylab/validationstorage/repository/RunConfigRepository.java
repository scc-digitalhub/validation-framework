package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.RunConfig;

public interface RunConfigRepository extends JpaRepository<RunConfig, String> {
    List<RunConfig> findByProjectIdAndExperimentId(String projectId, String experimentId);
}
