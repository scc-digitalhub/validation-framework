package it.smartcommunitylab.validationstorage.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.SchemaDTO;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.repository.DataPackageRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.SchemaRepository;
import it.smartcommunitylab.validationstorage.repository.StoreRepository;

public class DataResourceService {
    @Autowired
    private DataPackageRepository dataPackageRepository;
    
    @Autowired
    private StoreRepository storeRepository;
    
    @Autowired
    private DataResourceRepository dataResourceRepository;
    
    @Autowired
    private SchemaRepository schemaRepository;
    
    // Package
    public DataPackageDTO createDataPackage(String projectId, DataPackageDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public List<DataPackageDTO> findDataPackages(String projectId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public DataPackageDTO findDataPackageById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public DataPackageDTO findFrictionlessDataPackageById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataPackageDTO updateDataPackage(String projectId, String id, DataPackageDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteDataPackage(String projectId, String id) {
        // TODO Auto-generated method stub
    }
    
    // Store
    public StoreDTO createStore(String projectId, StoreDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public List<StoreDTO> findStores(String projectId) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public StoreDTO findStoreById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public StoreDTO updateStore(String projectId, String id, StoreDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteStore(String projectId, String id) {
        // TODO Auto-generated method stub
    }
    
    // Resource
    public DataResourceDTO createDataResource(String projectId, DataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public List<DataResourceDTO> findDataResources(String projectId) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public DataResourceDTO findDataResourceById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
    
    public DataResourceDTO findFrictionlessDataResourceById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataResourceDTO updateDataResource(String projectId, String id, DataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteDataResource(String projectId, String id) {
        // TODO Auto-generated method stub
    }
    
    // Schema
    public SchemaDTO createSchema(SchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public SchemaDTO findSchemaById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public SchemaDTO updateSchema(String id, SchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteSchema(String id) {
        // TODO Auto-generated method stub
    }
}
