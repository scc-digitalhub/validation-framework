package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.repository.DataPackageRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.StoreRepository;

@Service
public class DataResourceService {
    @Autowired
    private DataPackageRepository dataPackageRepository;
    
    @Autowired
    private StoreRepository storeRepository;
    
    @Autowired
    private DataResourceRepository dataResourceRepository;
    
    DataPackage searchDataPackage(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataPackage> o = dataPackageRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataPackage retrieveDataPackage(String id) {
        DataPackage document = searchDataPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Package '" + id + "' was not found.");
        
        return document;
    }
    
    private DataPackage searchDataPackageByName(String projectId, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(name))
            return null;
        
        Optional<DataPackage> o = dataPackageRepository.findByProjectIdAndName(projectId, name);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataPackage retrieveDataPackageByName(String projectId, String name) {
        DataPackage document = searchDataPackageByName(projectId, name);
        
        if (document == null)
            throw new DocumentNotFoundException("Package '" + name + "' under project '" + projectId + "' was not found.");
        
        return document;
    }
    
    private Store searchStore(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<Store> o = storeRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Store retrieveStore(String id) {
        Store document = searchStore(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Store '" + id + "' was not found.");
        
        return document;
    }
    
    private Store searchStoreByName(String projectId, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(name))
            return null;
        
        Optional<Store> o = storeRepository.findByProjectIdAndName(projectId, name);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Store searchDefaultStore(String projectId) {
        if (ObjectUtils.isEmpty(projectId))
            return null;
        
        List<Store> l = storeRepository.findByProjectIdAndIsDefault(projectId, true);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private DataResource searchDataResource(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataResource> o = dataResourceRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataResource retrieveDataResource(String id) {
        DataResource document = searchDataResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Resource '" + id + "' was not found.");
        
        return document;
    }
    
    private DataResource searchDataResourceByName(String projectId, String packageName, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(packageName) || ObjectUtils.isEmpty(name))
            return null;
        
        Optional<DataResource> o = dataResourceRepository.findByProjectIdAndPackageNameAndName(projectId, packageName, name);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    // Package
    public DataPackageDTO createDataPackage(String projectId, DataPackageDTO request) {
        String id = request.getId();
        if (id != null) {
            if (searchDataPackage(id) != null)
                throw new DocumentAlreadyExistsException("Package '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (searchDataPackageByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Package '" + name + "' under project '" + projectId + "' already exists.");
        
        DataPackage document = DataPackageDTO.to(request, projectId);
        document = savePackageWithItsResources(document);
        
        return DataPackageDTO.from(document);
    }
    
    DataPackage savePackageWithItsResources(DataPackage dataPackage) {
        List<DataResource> resources = dataResourceRepository.findByProjectIdAndPackageName(dataPackage.getProjectId(), dataPackage.getName());
    
        for (DataResource r : resources) {
            r.addPackage(dataPackage);
        }
        
        dataPackage.setResources(resources);
        
        dataPackage = dataPackageRepository.save(dataPackage);
                
        dataResourceRepository.saveAll(resources);
        
        return dataPackage;
    }
   
    public List<DataPackageDTO> findDataPackages(String projectId) {
        List<DataPackageDTO> dtos = new ArrayList<DataPackageDTO>();

        Iterable<DataPackage> results = dataPackageRepository.findByProjectId(projectId);
        
        for (DataPackage r : results) {
            dtos.add(DataPackageDTO.from(r));
        }

        return dtos;
    }
    
    public DataPackageDTO findDataPackageById(String projectId, String id) {
        DataPackage document = retrieveDataPackage(id);
        
        return DataPackageDTO.from(document);
    }
    
    public DataPackageDTO findFrictionlessDataPackageById(String projectId, String id) {
        // TODO
        DataPackage document = retrieveDataPackage(id);
        
        return DataPackageDTO.from(document);
    }
   
    public DataPackageDTO updateDataPackage(String projectId, String id, DataPackageDTO request) {
        DataPackage document = retrieveDataPackage(id);
        
        document.setTitle(request.getTitle());
        document.setType(request.getType());
        
        document = dataPackageRepository.save(document);
        
        return DataPackageDTO.from(document);
    }
   
    public void deleteDataPackage(String projectId, String id) {
        DataPackage document = retrieveDataPackage(id);
        
        List<DataResource> resources = document.getResources();
        
        for (DataResource r : resources) {
            r.removePackage(document);
        }
        
        dataResourceRepository.saveAll(resources);
        
        dataPackageRepository.deleteById(id);
    }
    
    // Store
    public StoreDTO createStore(String projectId, StoreDTO request) {
        String id = request.getId();
        if (id != null) {
            if (searchStore(id) != null)
                throw new DocumentAlreadyExistsException("Store '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (searchStoreByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Store '" + name + "' under project '" + projectId + "' already exists.");
        
        Store document = new Store();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setName(request.getName());
        document.setTitle(request.getTitle());
        document.setUri(request.getUri());
        document.setConfig(request.getConfig());
        
        Boolean isDefault = request.getIsDefault();
        Store currentDefault = searchDefaultStore(projectId);
        
        if (currentDefault == null) {
            if (isDefault == null || isDefault) {
                document.setIsDefault(true);
            } else {
                document.setIsDefault(false);
            }
        } else {
            document.setIsDefault(isDefault);
            if (isDefault != null && isDefault) {
                currentDefault.setIsDefault(false);
                storeRepository.save(currentDefault);
            }
        }
        
        document = storeRepository.save(document);
        
        return StoreDTO.from(document);
    }
    
    public List<StoreDTO> findStores(String projectId) {
        List<StoreDTO> dtos = new ArrayList<StoreDTO>();

        Iterable<Store> results = storeRepository.findByProjectId(projectId);
        
        for (Store r : results) {
            dtos.add(StoreDTO.from(r));
        }

        return dtos;
    }
   
    public StoreDTO findStoreById(String projectId, String id) {
        Store document = retrieveStore(id);
        
        return StoreDTO.from(document);
    }
   
    public StoreDTO updateStore(String projectId, String id, StoreDTO request) {
        Store document = retrieveStore(id);
        
        document.setTitle(request.getTitle());
        document.setUri(request.getUri());
        document.setConfig(request.getConfig());
        
        Boolean isDefault = request.getIsDefault();
        document.setIsDefault(isDefault);
        
        Store currentDefault = searchDefaultStore(projectId);
        
        if (isDefault != null && isDefault && currentDefault != null && !currentDefault.getId().equals(id)) {
            currentDefault.setIsDefault(false);
            storeRepository.save(currentDefault);
        }
        
        document = storeRepository.save(document);
        
        return StoreDTO.from(document);
    }
   
    public void deleteStore(String projectId, String id) {
        retrieveStore(id);
        System.out.println("Retrieved store " + id);
        List<DataResource> resources = dataResourceRepository.findByStoreId(id);
        System.out.println("Found resources: " + resources);
        for (DataResource r : resources) {
            System.out.println("Deleting resource " + r);
            deleteDataResource(projectId, r.getId());
        }
        System.out.println("Deleted the store's resources");
        storeRepository.deleteById(id);
    }
    
    // Resource
    public DataResourceDTO createDataResource(String projectId, DataResourceDTO request) {
        String id = request.getId();
        if (request.getId() != null) {
            if (searchDataResource(id) != null)
                throw new DocumentAlreadyExistsException("Resource '" + id + "' already exists.");
        }
        
        String packageName = request.getPackageName();
        String name = request.getName();
        if (searchDataResourceByName(projectId, packageName, name) != null)
            throw new DocumentAlreadyExistsException("Resource '" + name + "' under project '" + projectId + "', package '" + packageName + "' already exists.");
        
        DataPackage dataPackage = retrieveDataPackageByName(projectId, packageName);
        
        Store defaultStore = searchDefaultStore(projectId);
        String defaultStoreId = null;
        if (defaultStore != null)
            defaultStoreId = defaultStore.getId();
        
        DataResource document = DataResourceDTO.to(request, projectId, dataPackage, defaultStoreId);
        
        document = dataResourceRepository.save(document);
        
        if (dataPackage != null) {
            dataPackage.addResource(document);
            dataPackageRepository.save(dataPackage);
        }
        
        return DataResourceDTO.from(document);
    }
   
    public List<DataResourceDTO> findDataResources(String projectId) {
        List<DataResourceDTO> dtos = new ArrayList<DataResourceDTO>();

        Iterable<DataResource> results = dataResourceRepository.findByProjectId(projectId);
        
        for (DataResource r : results) {
            dtos.add(DataResourceDTO.from(r));
        }

        return dtos;
    }
    
    public DataResourceDTO findDataResourceById(String projectId, String id) {
        DataResource document = retrieveDataResource(id);
        
        return DataResourceDTO.from(document);
    }
    
    public DataResourceDTO findFrictionlessDataResourceById(String projectId, String id) {
        // TODO
        DataResource document = retrieveDataResource(id);
        
        return DataResourceDTO.from(document);
    }
   
    public DataResourceDTO updateDataResource(String projectId, String id, DataResourceDTO request) {
        DataResource document = retrieveDataResource(id);
        
        document.setStoreId(request.getStoreId());
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setType(request.getType());
        document.setSchema(request.getSchema());
        document.setDataset(request.getDataset());
        
        document = dataResourceRepository.save(document);
        
        return DataResourceDTO.from(document);
    }
   
    public void deleteDataResource(String projectId, String id) {
        retrieveDataResource(id);
        
        dataResourceRepository.deleteById(id);
    }
}
