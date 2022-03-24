package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.DataResource;

public interface DataResourceRepository extends CrudRepository<DataResource, String> {
    List<DataResource> findByProjectId(String projectId);
    
    List<DataResource> findByProjectIdAndPackageNameAndName(String projectId, String packageName, String name);
}
