package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentAlreadyExistsException;
import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import it.smartcommunitylab.validationstorage.model.Constraint;
import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.DataResource;
import it.smartcommunitylab.validationstorage.model.Run;
import it.smartcommunitylab.validationstorage.model.RunEnvironment;
import it.smartcommunitylab.validationstorage.model.Schema;
import it.smartcommunitylab.validationstorage.model.Store;
import it.smartcommunitylab.validationstorage.model.dto.ConstraintDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.model.dto.DataResourceDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunDTO;
import it.smartcommunitylab.validationstorage.model.dto.RunEnvironmentDTO;
import it.smartcommunitylab.validationstorage.model.dto.StoreDTO;
import it.smartcommunitylab.validationstorage.repository.DataPackageRepository;
import it.smartcommunitylab.validationstorage.repository.DataResourceRepository;
import it.smartcommunitylab.validationstorage.repository.StoreRepository;
import it.smartcommunitylab.validationstorage.typed.TypedConstraint;

@Service
public class DataResourceService {
    @Autowired
    private DataPackageRepository dataPackageRepository;
    
    @Autowired
    private StoreRepository storeRepository;
    
    @Autowired
    private DataResourceRepository dataResourceRepository;
    
    private DataPackage getDataPackage(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataPackage> o = dataPackageRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataPackage getDataPackageByName(String projectId, String name) {
        Optional<DataPackage> o = dataPackageRepository.findByProjectIdAndName(projectId, name);
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
    
    private Store getStoreByName(String projectId, String name) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(name))
            return null;
        
        Optional<Store> o = storeRepository.findByProjectIdAndName(projectId, name);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private Store getDefaultStore(String projectId) {
        if (ObjectUtils.isEmpty(projectId))
            return null;
        
        List<Store> l = storeRepository.findByProjectIdAndIsDefault(projectId, true);
        if (l.size() > 0) {
            return l.get(0);
        }
        
        return null;
    }
    
    private DataResource getDataResource(String id) {
        if (ObjectUtils.isEmpty(id))
            return null;

        Optional<DataResource> o = dataResourceRepository.findById(id);
        if (o.isPresent()) {
            return o.get();
        }
        
        return null;
    }
    
    private DataResource getDataResourceByName(String projectId, String packageName, String name) {
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
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        String id = request.getId();
        if (id != null) {
            if (getDataPackage(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (getDataPackageByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "' already exists.");
        
        DataPackage document = new DataPackage();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setName(name);
        document.setTitle(request.getTitle());
        document.setType(request.getType());
        
        List<DataResource> resourcesCreatedBeforePackage = dataResourceRepository.findByProjectIdAndPackageName(projectId, name);
        
        for (DataResource r : resourcesCreatedBeforePackage) {
            r.addPackage(document);
        }
        
        document.setResources(resourcesCreatedBeforePackage);
        
        dataPackageRepository.save(document);
        
        dataResourceRepository.saveAll(resourcesCreatedBeforePackage);
        
        return DataPackageDTO.from(document);
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
        DataPackage document = getDataPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return DataPackageDTO.from(document);
    }
    
    public DataPackageDTO findFrictionlessDataPackageById(String projectId, String id) {
        // TODO
        DataPackage document = getDataPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return DataPackageDTO.from(document);
    }
   
    public DataPackageDTO updateDataPackage(String projectId, String id, DataPackageDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        DataPackage document = getDataPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        document.setTitle(request.getTitle());
        document.setType(request.getType());
        
        dataPackageRepository.save(document);
        
        return DataPackageDTO.from(document);
    }
   
    public void deleteDataPackage(String projectId, String id) {
        DataPackage document = getDataPackage(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        List<DataResource> resources = document.getResources();
        
        for (DataResource r : resources) {
            r.removePackage(document);
        }
        
        dataResourceRepository.saveAll(resources);
        
        dataPackageRepository.deleteById(id);
    }
    
    void deleteRunDataPackage(String projectId, String name) {
        DataPackage document = getDataPackageByName(projectId, name);
        
        if (document == null)
            throw new DocumentNotFoundException("Document '" + name + "' under project '" + projectId + "' was not found.");
        
        List<DataResource> resources = document.getResources();
        
        for (DataResource r : resources) {
            r.removePackage(document);
        }
        
        dataResourceRepository.saveAll(resources);
        
        dataPackageRepository.deleteByProjectIdAndNameAndType(projectId, name, "run");
    }
    
    // Store
    public StoreDTO createStore(String projectId, StoreDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        String id = request.getId();
        if (id != null) {
            if (getStore(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        } else {
            id = UUID.randomUUID().toString();
        }
        
        String name = request.getName();
        if (getStoreByName(projectId, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "' already exists.");
        
        Store document = new Store();
        
        document.setId(id);
        document.setProjectId(projectId);
        document.setName(request.getName());
        document.setTitle(request.getTitle());
        document.setUri(request.getUri());
        document.setConfig(request.getConfig());
        
        Boolean isDefault = request.getIsDefault();
        Store currentDefault = getDefaultStore(projectId);
        
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
        
        storeRepository.save(document);
        
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
        Store document = getStore(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return StoreDTO.from(document);
    }
   
    public StoreDTO updateStore(String projectId, String id, StoreDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        Store document = getStore(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        document.setTitle(request.getTitle());
        document.setUri(request.getUri());
        document.setConfig(request.getConfig());
        
        Boolean isDefault = request.getIsDefault();
        document.setIsDefault(isDefault);
        
        Store currentDefault = getDefaultStore(projectId);
        
        if (isDefault != null && isDefault && currentDefault != null && !currentDefault.getId().equals(id)) {
            currentDefault.setIsDefault(false);
            storeRepository.save(currentDefault);
        }
        
        storeRepository.save(document);
        
        return StoreDTO.from(document);
    }
   
    public void deleteStore(String projectId, String id) {
        Store document = getStore(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        List<DataResource> resources = dataResourceRepository.findByStoreId(id);
        for (DataResource r : resources) {
            deleteDataResource(projectId, r.getId());
        }
        
        storeRepository.deleteById(id);
    }
    
    // Resource
    public DataResourceDTO createDataResource(String projectId, DataResourceDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        String id = request.getId();
        if (request.getId() != null) {
            if (getDataResource(id) != null)
                throw new DocumentAlreadyExistsException("Document with id '" + id + "' already exists.");
        }
        
        String packageName = request.getPackageName();
        String name = request.getName();
        if (getDataResourceByName(projectId, packageName, name) != null)
            throw new DocumentAlreadyExistsException("Document '" + name + "' under project '" + projectId + "', package '" + packageName + "' already exists.");
        
        DataPackage dataPackage = getDataPackageByName(projectId, packageName);
        
        Store defaultStore = getDefaultStore(projectId);
        String defaultStoreId = null;
        if (defaultStore != null)
            defaultStoreId = defaultStore.getId();
        
        DataResource document = DataResourceDTO.to(request, dataPackage, defaultStoreId);
        document.setProjectId(projectId);
        
        dataResourceRepository.save(document);
        
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
        DataResource document = getDataResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return DataResourceDTO.from(document);
    }
    
    public DataResourceDTO findFrictionlessDataResourceById(String projectId, String id) {
        // TODO
        DataResource document = getDataResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return DataResourceDTO.from(document);
    }
   
    public DataResourceDTO updateDataResource(String projectId, String id, DataResourceDTO request) {
        ValidationStorageUtils.checkIdMatch(projectId, request.getProjectId());
        
        DataResource document = getDataResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        document.setStoreId(request.getStoreId());
        document.setTitle(request.getTitle());
        document.setDescription(request.getDescription());
        document.setType(request.getType());
        document.setSchema(request.getSchema());
        document.setDataset(request.getDataset());
        
        dataResourceRepository.save(document);
        
        return DataResourceDTO.from(document);
    }
   
    public void deleteDataResource(String projectId, String id) {
        DataResource document = getDataResource(id);
        
        if (document == null)
            throw new DocumentNotFoundException("Document with ID '" + id + "' was not found.");
        
        dataResourceRepository.deleteById(id);
    }
}
