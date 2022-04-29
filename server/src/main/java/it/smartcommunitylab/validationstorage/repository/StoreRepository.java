package it.smartcommunitylab.validationstorage.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.Store;

public interface StoreRepository extends JpaRepository<Store, String> {
    
    List<Store> findByProjectId(String projectId);
    
    Optional<Store> findByProjectIdAndName(String projectId, String name);

    List<Store> findByProjectIdAndIsDefault(String projectId, Boolean b);
    
}
