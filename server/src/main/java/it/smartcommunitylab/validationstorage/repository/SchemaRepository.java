package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Schema;

public interface SchemaRepository extends CrudRepository<Schema, String> {

}
