package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.RunConfig;

public interface RunConfigRepository extends CrudRepository<RunConfig, String> {

}
