package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Constraint;

public interface ConstraintRepository extends CrudRepository<Constraint, String> {
    List<Constraint> findByProjectIdAndExperimentId(String projectId, String experimentId);
    
    List<Constraint> findByExperimentId(String experimentId);
}
