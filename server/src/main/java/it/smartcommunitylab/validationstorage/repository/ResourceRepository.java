package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.DataResource;

public interface ResourceRepository extends CrudRepository<DataResource, String> {

}
