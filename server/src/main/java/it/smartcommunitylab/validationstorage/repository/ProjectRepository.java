package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.Project;

public interface ProjectRepository extends CrudRepository<Project, String> {
    
}