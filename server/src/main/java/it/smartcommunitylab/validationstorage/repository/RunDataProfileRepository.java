package it.smartcommunitylab.validationstorage.repository;

import it.smartcommunitylab.validationstorage.model.RunDataProfile;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.CrudRepository;

public interface RunDataProfileRepository extends CrudRepository<RunDataProfile, String> {
    List<RunDataProfile> findByProjectId(String projectId);

    List<RunDataProfile> findByProjectIdAndExperimentId(String projectId, String experimentId);

    List<RunDataProfile> findByProjectIdAndRunId(String projectId, String runId);

    List<RunDataProfile> findByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);

    void deleteByProjectId(String projectId);

    void deleteByProjectIdAndExperimentId(String projectId, String experimentId);

    void deleteByProjectIdAndRunId(String projectId, String runId);

    void deleteByProjectIdAndExperimentIdAndRunId(String projectId, String experimentId, String runId);
}