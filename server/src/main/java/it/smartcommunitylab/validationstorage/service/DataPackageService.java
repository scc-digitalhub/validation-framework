package it.smartcommunitylab.validationstorage.service;

import java.util.List;
import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylab.validationstorage.model.DataPackage;
import it.smartcommunitylab.validationstorage.model.dto.DataPackageDTO;
import it.smartcommunitylab.validationstorage.repository.DataPackageRepository;

public class DataPackageService {
    @Autowired
    private DataPackageRepository repository;
    
    public DataPackage create(String projectId, @Valid DataPackageDTO request, String name) {
        // TODO Auto-generated method stub
        return null;
    }

    public List<DataPackage> findByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId, Optional<String> search) {
        // TODO Auto-generated method stub
        return null;
    }

    public DataPackage findById(String projectId, String id) {
        // TODO Auto-generated method stub
        return null;
    }

    public DataPackage update(String projectId, String id, @Valid DataPackageDTO request) {
        // TODO Auto-generated method stub
        return null;
    }

    public void deleteById(String projectId, String id) {
        // TODO Auto-generated method stub
    }

    public void deleteByProjectId(String projectId, Optional<String> experimentId, Optional<String> runId) {
        // TODO Auto-generated method stub
    }
}
