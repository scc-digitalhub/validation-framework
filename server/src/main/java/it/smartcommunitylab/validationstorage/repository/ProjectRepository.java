package it.smartcommunitylab.validationstorage.repository;

import java.util.Set;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.Project;

public interface ProjectRepository extends JpaRepository<Project, String> {

    Page<Project> findByNameIn(Set<String> projectNames, Pageable pageable);
    
}