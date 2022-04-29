package it.smartcommunitylab.validationstorage.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import it.smartcommunitylab.validationstorage.model.DataResource;

public interface DataResourceRepository extends JpaRepository<DataResource, String> {
    List<DataResource> findByProjectId(String projectId);
    
    Optional<DataResource> findByProjectIdAndPackageNameAndName(String projectId, String packageName, String name);

    List<DataResource> findByStoreId(String storeId);

    List<DataResource> findByProjectIdAndPackageName(String projectId, String name);
}
