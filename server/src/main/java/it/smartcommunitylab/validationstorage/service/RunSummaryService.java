package it.smartcommunitylab.validationstorage.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import it.smartcommunitylab.validationstorage.common.DocumentNotFoundException;
import it.smartcommunitylab.validationstorage.model.DataProfile;
import it.smartcommunitylab.validationstorage.model.RunMetadata;
import it.smartcommunitylab.validationstorage.model.RunSummary;
import it.smartcommunitylab.validationstorage.model.ShortReport;
import it.smartcommunitylab.validationstorage.repository.DataProfileRepository;
import it.smartcommunitylab.validationstorage.repository.RunMetadataRepository;
import it.smartcommunitylab.validationstorage.repository.ShortReportRepository;

/**
 * Service for run summaries.
 */
@Service
public class RunSummaryService {
    @Autowired
    private RunMetadataRepository runMetadataRepository;
    @Autowired
    private ShortReportRepository shortReportRepository;
    @Autowired
    private DataProfileRepository dataProfileRepository;
    
    /**
     * Returns a list of run summaries for the provided experiment
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param pageable Pageable.
     * @return List of run summaries.
     */
    public List<RunSummary> listBasicRunSummaries(String projectId, String experimentId, Pageable pageable) {
        List<RunMetadata> runMetadataDocuments = runMetadataRepository.findByProjectIdAndExperimentId(projectId, experimentId, pageable);
        return buildRunSummaryListFromRunMetadataDocuments(projectId, experimentId, runMetadataDocuments);
    }
    
    /**
     * Returns the most recent run summaries for the given experiment.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @return List of recent run summaries.
     */
    public List<RunSummary> getRichRecentRunSummaries(String projectId, String experimentId) {
        Pageable pageable = PageRequest.of(0, 5, Sort.by("created").descending());
        List<RunSummary> runSummaries = listBasicRunSummaries(projectId, experimentId, pageable);
        enrichRunSummaries(runSummaries);
        
        return runSummaries;
    }
    
    /** Enriches each run summary with additional documents.
     * 
     * @param projectId Project ID
     * @param experimentId Experiment ID.
     * @param runSummaries List of run summaries.
     */
    private void enrichRunSummaries(List<RunSummary> runSummaries) {
        for (RunSummary run : runSummaries)
            run.setDataProfile(getDataProfile(run.getProjectId(), run.getExperimentId(), run.getRunId()));
    }
    
    /**
     * Returns a list of run summaries, built from the list of provided RunMetadata document IDs.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param runMetadataIds RunMetadata IDs.
     * @return List of run summaries.
     */
    public List<RunSummary> getRichRunSummariesByRunMetadataIds(String projectId, String experimentId, String[] runMetadataIds) {
        List<RunMetadata> runMetadataDocuments = getAndCheckRunMetadataDocuments(projectId, experimentId, runMetadataIds);
        List<RunSummary> runSummaries = buildRunSummaryListFromRunMetadataDocuments(projectId, experimentId, runMetadataDocuments);
        enrichRunSummaries(runSummaries);
        
        return runSummaries;
    }
    
    /**
     * Retrieves the list of RunMetadata documents that match the provided list of document IDs.
     * If a RunMetadata document does not match the input project ID or experiment ID, throws an error.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param runMetadataIds List of RunMetadata document IDs.
     * @return List of RunMetadata documents.
     */
    private List<RunMetadata> getAndCheckRunMetadataDocuments(String projectId, String experimentId, String[] runMetadataIds) {
        if (ObjectUtils.isEmpty(projectId) || ObjectUtils.isEmpty(experimentId))
            throw new IllegalArgumentException("Project ID or experiment ID are required and cannot be blank.");
        if (ObjectUtils.isEmpty(runMetadataIds))
            throw new IllegalArgumentException("No document IDs have been provided.");
        
        List<RunMetadata> documents;
        
        documents = new ArrayList<RunMetadata>();
        for (String runMetadataId: runMetadataIds) {
            RunMetadata document = getRunMetadataById(runMetadataId);
            
            if (!document.getProjectId().equals(projectId) || !document.getExperimentId().equals(experimentId))
                throw new IllegalArgumentException("Specified project ID or experiment ID do not match the values contained in the document.");
                
            documents.add(document);
        }
        
        return documents;
    }
    
    /**
     * Returns a list of run summaries built from the provided RunMetadata documents.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param runMetadataDocuments RunMetadata documents.
     * @return List of run summaries.
     */
    private List<RunSummary> buildRunSummaryListFromRunMetadataDocuments(String projectId, String experimentId, List<RunMetadata> runMetadataDocuments) {
        runMetadataDocuments.sort((a,b)->b.getCreated().compareTo(a.getCreated()));;
        
        List<RunSummary> runs = new ArrayList<RunSummary>();
        
        for (RunMetadata runMetadata: runMetadataDocuments)
            runs.add(buildRunSummaryFromRunMetadataDocument(projectId, experimentId, runMetadata));
        
        return runs;
    }
    
    /**
     * Returns a run summary built from the provided RunMetadata document.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param runMetadata RunMetadata document.
     * @return A run summary.
     */
    private RunSummary buildRunSummaryFromRunMetadataDocument(String projectId, String experimentId, RunMetadata runMetadata) {
        String runId = runMetadata.getRunId();
        
        ShortReport shortReport = getShortReport(projectId, experimentId, runId);
        
        RunSummary runSummary = new RunSummary(runMetadata.getId(), projectId, experimentId, runId, runMetadata.getCreated());
        
        runSummary.setRunMetadata(runMetadata);
        runSummary.setShortReport(shortReport);
        
        return runSummary;
    }
    
    /**
     * Returns a run summary.
     * @param projectId Project ID.
     * @param experimentId Experiment ID.
     * @param runId Run ID.
     * @return A run summary.
     */
    public RunSummary getBasicRunSummary(String projectId, String experimentId, String runId) {
        RunMetadata runMetadata = getRunMetadata(projectId, experimentId, runId);
        return buildRunSummaryFromRunMetadataDocument(projectId, experimentId, runMetadata);
    }
    
    /**
     * Obtains RunMetadata document by ID.
     * @param id Document ID.
     * @return RunMetadata.
     */
    private RunMetadata getRunMetadataById(String id) {
        if (ObjectUtils.isEmpty(id))
            throw new IllegalArgumentException("Document ID must have a value.");
        
        Optional<RunMetadata> document = runMetadataRepository.findById(id);
        if (!document.isPresent())
            throw new DocumentNotFoundException("Document with ID " + id + " was not found.");
        
        return document.get();
    }
    
    /**
     * Obtains RunMetadata document by project ID, experiment ID and run ID.
     * @param projectId ProjectID.
     * @param experimentId ExperimentID.
     * @param runId RunID.
     * @return RunMetadata document.
     */
    private RunMetadata getRunMetadata(String projectId, String experimentId, String runId) {
        List<RunMetadata> documents = runMetadataRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        return null;
    }
    
    /**
     * Obtains ShortReport document.
     * @param projectId ProjectID.
     * @param experimentId ExperimentID.
     * @param runId RunID.
     * @return ShortReport document.
     */
    private ShortReport getShortReport(String projectId, String experimentId, String runId) {
        List<ShortReport> documents = shortReportRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        return null;
    }
    
    /**
     * Obtains ShortReport document.
     * @param projectId ProjectID.
     * @param experimentId ExperimentID.
     * @param runId RunID.
     * @return ShortReport document.
     */
    private DataProfile getDataProfile(String projectId, String experimentId, String runId) {
        List<DataProfile> documents = dataProfileRepository.findByProjectIdAndExperimentIdAndRunId(projectId, experimentId, runId);
        if (!documents.isEmpty())
            return documents.get(0);
        return null;
    }
}
