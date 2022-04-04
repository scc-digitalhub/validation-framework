package it.smartcommunitylab.validationstorage.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Experiment;

public interface ExperimentRepository extends CrudRepository<Experiment, String> {
    
    List<Experiment> findByProjectId(String projectId);

    List<Experiment> findByProjectId(String projectId, Pageable pageable);
    
    List<Experiment> findByProjectIdAndTagsIn(String projectId, List<String> tags, Pageable pageable);

    Optional<Experiment> findByProjectIdAndName(String projectId, String Name);

    void deleteByProjectId(String projectId);

}