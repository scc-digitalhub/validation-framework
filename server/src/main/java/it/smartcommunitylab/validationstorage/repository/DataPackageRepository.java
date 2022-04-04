package it.smartcommunitylab.validationstorage.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.repository.CrudRepository;

import it.smartcommunitylab.validationstorage.model.DataPackage;

public interface DataPackageRepository extends CrudRepository<DataPackage, String> {
    
    List<DataPackage> findByProjectId(String projectId);
    
    Optional<DataPackage> findByProjectIdAndName(String projectId, String name);
    
    List<DataPackage> findByProjectIdAndType(String projectId, String type);

    DataPackage findByProjectIdAndNameAndType(String projectId, String name, String type);
    
    void deleteByProjectIdAndNameAndType(String projectId, String name, String type);

}
