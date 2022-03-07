package it.smartcommunitylab.validationstorage.repository;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.DataPackage;

public interface DataPackageRepository extends CrudRepository<DataPackage, String> {
    
    List<DataPackage> findByProjectId(String projectId);

}
