package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.Run;

public interface RunRepository extends JpaRepository<Run, String> {
    
    List<Run> findByProjectIdAndExperimentId(String projectId, String experimentId);
    
    List<Run> findByExperimentId(String experimentId);
    
    List<Run> findByExperimentId(String experimentId, Pageable pageable);
    
    void deleteByProjectId(String projectId);
    
    void deleteByExperimentId(String experimentId);
    
    void deleteByProjectIdAndExperimentIdAndId(String projectId, String experimentId, String id);
    
}
