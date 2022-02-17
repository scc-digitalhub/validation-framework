package it.smartcommunitylab.validationstorage.service;

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
    public DataPackageDTO createDataPackage(DataPackageDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataPackageDTO findDataPackageById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataPackageDTO updateDataPackage(String id, DataPackageDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteDataPackage(String id) {
        // TODO Auto-generated method stub
    }
    
    // Store
    public StoreDTO createStore(StoreDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public StoreDTO findStoreById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public StoreDTO updateStore(String id, StoreDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteStore(String id) {
        // TODO Auto-generated method stub
    }
    
    // Resource
    public DataResourceDTO createDataResource(DataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataResourceDTO findDataResourceById(String id) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public DataResourceDTO updateDataResource(String id, DataResourceDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteDataResource(String id) {
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
