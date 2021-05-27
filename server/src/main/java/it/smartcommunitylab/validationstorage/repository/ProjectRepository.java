package it.smartcommunitylab.validationstorage.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import it.smartcommunitylab.validationstorage.model.Project;

public interface ProjectRepository extends MongoRepository<Project, String> {
}