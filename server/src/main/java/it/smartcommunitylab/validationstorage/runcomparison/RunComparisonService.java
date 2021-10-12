package it.smartcommunitylab.validationstorage.runcomparison;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.model.DataProfile;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.repository.DataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RunComparisonService {
    private final RunMetadataRepository runMetadataRepository;
    private final DataProfileRepository dataProfileRepository;
    private final ShortReportRepository shortReportRepository;
    
    /**
     * Returns a map for comparing runs that belong to the same project and experiment.
     * @param projectId Project ID
     * @param experimentId Experiment ID
     * @param runMetadataIds RunMetadata IDs
     * @return A map for comparing runs
     */
    public RunComparison getComparison(String projectId, String experimentId, String[] runMetadataIds) {
        List<RunMetadata> runMetadataDocuments = getAndCheckRunMetadataDocuments(projectId, experimentId, runMetadataIds);
        
        runMetadataDocuments.sort((a,b)->b.getCreated().compareTo(a.getCreated()));;
        
        List<RunSummary> runs = new ArrayList<RunSummary>();
        
        for (RunMetadata runMetadata: runMetadataDocuments) {
            String runId = runMetadata.getRunId();
            
            ShortReport shortReport = getShortReport(projectId, experimentId, runId);
            DataProfile dataProfile = getDataProfile(projectId, experimentId, runId);
            
            RunSummary runSummary = new RunSummary(runMetadata.getId(), projectId, experimentId, runId, runMetadata.getCreated());
            
            runSummary.setRunMetadata(runMetadata);
            runSummary.setShortReport(shortReport);
            runSummary.setDataProfile(dataProfile);
            
            runs.add(runSummary);
        }
        
        return new RunComparison(String.join(",", runMetadataIds), projectId, experimentId, runMetadataIds, runs);
    }

    private List<RunMetadata> getAndCheckRunMetadataDocuments(String projectId, String experimentId, String[] ids) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId))
            throw new IllegalArgumentException("Project ID or experiment ID are null or blank. Unable to verify if the requested documents belong to the experiment.");
        if (ObjectUtils.isEmpty(ids))
            throw new IllegalArgumentException("No document IDs have been provided.");
        
        List<RunMetadata> documents;
        
        if (ids.length >= 2) {
            documents = new ArrayList<RunMetadata>();
            for (String id: ids) {
                RunMetadata document = getRunMetadataDocument(id);
                
                if (!document.getProjectId().equals(projectId) || !document.getExperimentId().equals(experimentId))
                    throw new IllegalArgumentException("Specified project ID or experiment ID do not match the values contained in the document.");
                    
                documents.add(document);
            }
        } else if (ids.length == 1 && ids[0].equals(ValidationStorageConstants.RUN_COMPARISON_RECENT)) {
            Pageable pageable = PageRequest.of(0, 5, Sort.by("created").descending()); 
            
            documents = runMetadataRepository.findByProjectIdAndExperimentId(projectId, experimentId, pageable);
        } else
            throw new IllegalArgumentException("At least 2 document IDs are necessary for a comparison.");
        
        return documents;
    }

    private RunMetadata getRunMetadataDocument(String id) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID must have a value");
        
        Optional<RunMetadata> document = runMetadataRepository.findById(id);
        if (!document.isPresent())
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return document.get();
    }
    
    private ShortReport getShortReport(String projectId, String experimentId, String runId) {
        List<ShortReport> runInArray = shortReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);

        if (!ObjectUtils.isEmpty(runInArray))
            return runInArray.get(0);
        
        return null;
    }
    
    private DataProfile getDataProfile(String projectId, String experimentId, String runId) {
        List<DataProfile> runInArray = dataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);

        if (!ObjectUtils.isEmpty(runInArray))
            return runInArray.get(0);
        
        return null;
    }
}
