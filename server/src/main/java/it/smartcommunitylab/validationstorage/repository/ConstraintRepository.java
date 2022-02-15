package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Constraint;

public interface ConstraintRepository extends CrudRepository<Constraint, String> {

}
