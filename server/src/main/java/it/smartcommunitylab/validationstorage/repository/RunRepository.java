package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Run;

public interface RunRepository extends CrudRepository<Run, String> {

}
