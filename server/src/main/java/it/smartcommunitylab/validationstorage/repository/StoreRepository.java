package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Store;

public interface StoreRepository extends CrudRepository<Store, String> {
    
    List<Store> findByProjectId(String projectId);
    
}
