package it.smartcommunitylab.validationstorage.service;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.Schema;
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
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
    
    private DataPackage getPackage(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataPackage> o = dataPackageRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Store getStore(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Store> o = storeRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataResource getResource(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataResource> o = dataResourceRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Schema getSchema(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Schema> o = schemaRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataPackageDTO makeDTO(DataPackage source) {
        DataPackageDTO dto = new DataPackageDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        
        Set<String> resourceIds = new HashSet<String>();
        for (DataResource i : source.getResources()) {
            resourceIds.add(i.getId());
        }
        dto.setResourceIds(resourceIds);
        
        return dto;
    }
    
    private StoreDTO makeDTO(Store source) {
        StoreDTO dto = new StoreDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setPath(source.getPath());
        dto.setConfig(source.getConfig());
        dto.setIsDefault(source.getIsDefault());
        dto.setResources(null);
        
        return dto;
    }
    
    private DataResourceDTO makeDTO(DataResource source) {
        DataResourceDTO dto = new DataResourceDTO();
        
        dto.setId(source.getId());
        dto.setProjectId(source.getProjectId());
        dto.setPackageId(source.getPackageId());
        dto.setStoreId(source.getStoreId());
        dto.setName(source.getName());
        dto.setTitle(source.getTitle());
        dto.setSchema(makeDTO(source.getSchema()));
        dto.setDataset(source.getDataset());
        
        return dto;
    }
    
    private SchemaDTO makeDTO(Schema source) {
        SchemaDTO dto = new SchemaDTO();
        
        dto.setId(source.getId());
        Optional<DataResource> o = dataResourceRepository.findById(source.getResourceId());
        if (o.isPresent()) {
            dto.setResource(makeDTO(o.get()));
        }
        
        return dto;
    }
    
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
        DataPackage document = getPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        ValidationStorageUtils.checkIdMatch(projectId, document.getProjectId());
        
        return makeDTO(document);
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
        dataPackageRepository.deleteById(id);
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
        Store document = getStore(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        ValidationStorageUtils.checkIdMatch(projectId, document.getProjectId());
        
        return makeDTO(document);
    }
   
    public StoreDTO updateStore(String projectId, String id, StoreDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteStore(String projectId, String id) {
        storeRepository.deleteById(id);
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
        DataResource document = getResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        ValidationStorageUtils.checkIdMatch(projectId, document.getProjectId());
        
        return makeDTO(document);
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
        dataResourceRepository.deleteById(id);
    }
    
    // Schema
    public SchemaDTO createSchema(SchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public SchemaDTO findSchemaById(String id) {
        Schema document = getSchema(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return makeDTO(document);
    }
   
    public SchemaDTO updateSchema(String id, SchemaDTO request) {
        // TODO Auto-generated method stub
        return null;
    }
   
    public void deleteSchema(String id) {
        schemaRepository.deleteById(id);
    }
}
