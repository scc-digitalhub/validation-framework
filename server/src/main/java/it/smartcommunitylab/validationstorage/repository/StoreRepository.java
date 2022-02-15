package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Store;

public interface StoreRepository extends CrudRepository<Store, String> {
    
}
