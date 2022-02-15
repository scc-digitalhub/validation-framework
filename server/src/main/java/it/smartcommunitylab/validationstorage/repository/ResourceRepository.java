package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Resource;

public interface ResourceRepository extends CrudRepository<Resource, String> {

}
