clear
% *** initializing the controlling parameters like deletionCount,...
% clusterCount, number of times hashing will be done *** %

deletionCount=100;
clusterCount=100;
hashCount=1;
loopStepSize=50;
countofRecordedValues=deletionCount/loopStepSize;
% *** reading the graph in edge list format with first two lines as... 
% nodeCount and edgeCount *** %

fileName='amazon';
fid = fopen(strcat('Datasets\',fileName,'.txt'));
formatSpec = '%d %d';
sizeA = [2 Inf];
edgeList = fscanf(fid, formatSpec,sizeA);
edgeList = edgeList';
fclose(fid);

walk6Time=zeros(countofRecordedValues,1);
walk8Time=zeros(countofRecordedValues,1);
nsTime= zeros(countofRecordedValues,1);

walk6EigenDropPercentage=zeros(countofRecordedValues,1);
walk8EigenDropPercentage=zeros(countofRecordedValues,1);
nsEigenDropPercentage= zeros(countofRecordedValues,1);

w6_greedySelectedNodes=zeros(deletionCount,1);
w8_greedySelectionNodes=zeros(deletionCount,1);

outputFileName=strcat(fileName,'_',num2str(hashCount),'_',...
    num2str(clusterCount),'_',num2str(deletionCount));

nodeCount=edgeList(1,1);
edgeList(1,:)=[];
edgeList = unique(sort(edgeList,2), 'rows');
edgeCount=length(edgeList);
% *** make the Adjacency matrix of graph *** %
G = graph(edgeList(:,1),edgeList(:,2));
matrix = adjacency(G);

nodeCount=G.numnodes;
matrixLength=nodeCount;
degree= full(sum(matrix));

X=zeros(deletionCount/loopStepSize,1);
Score_w6=[];
Score_w8=[];

%   *** calculating the largest eigen value of the graph **** %   
 opts.disp = 0;
 [u00, largestLam] = eigs(matrix, 1,'LM',opts);
 
 fprintf('Graph Name : %s\n',fileName);
 fprintf('Node Count : %d\n',nodeCount);
 fprintf('Edge Count : %d\n',edgeCount);
 fprintf('Lambda : %0.2f\n',largestLam);
 
for k=1:countofRecordedValues
    X(k)=k*loopStepSize;
end

%   **** Caculating Eigen Drop For NetSheild *** %

fprintf('Computing NetSheild...: \n');
i=0;
for k=1:countofRecordedValues
    
    [eigenDropPercent_ns,timeTaken_ns] = Netshield(matrix,k*loopStepSize,[]);        
    nsTime(k)= timeTaken_ns;
    nsEigenDropPercentage(k)=eigenDropPercent_ns;
    
end
fprintf('\t*** NetSheild Computed *** \n');

Scores_w6=zeros(hashCount,nodeCount);
Scores_w8=zeros(hashCount,nodeCount);

for y=1:hashCount
   tic;
   a=rand();
   b=rand();
   C=zeros(clusterCount,clusterCount);
%    [hash,clusterSizes,record] = calculateHashes(matrixLength,clusterCount,a,b);
   hash = ceil(rand(nodeCount,1)*clusterCount);
   u_id = 0;
   v_id = 0;
   
    for i=1:edgeCount
        u_id =  edgeList(i,1);
        v_id =  edgeList(i,2);
        
       clustID_u=hash(edgeList(i,1));
       clustID_v=hash(edgeList(i,2));
              
       C(clustID_u,clustID_v)=C(clustID_u,clustID_v)+1;
       if(clustID_u~=clustID_v)
           C(clustID_v,clustID_u)=C(clustID_v,clustID_u)+1;
       end
    end
   hashingTime=toc;
   fprintf('Hashing Time %0.2f\n',hashingTime);
   
   fprintf('Computing Walk_8 ...: \n');
%    [nodeScore_w8,scoreComputationTime_w8] = ...
%        Walk8_Algorithm(nodeCount,clusterCount,hash,C,degree);
   
   [nodeScore_w8,scoreComputationTime_w8] = ...
       Walk8_Algorithm(nodeCount,clusterCount,hash,C,degree);
   
   scoreComputationTime_w8= hashingTime+scoreComputationTime_w8;
   fprintf('Walk-8 Total Time : %0.2f\n',(scoreComputationTime_w8));
   fprintf('\t*** Computed Walk_8 *** \n');


   fprintf('Computing Walk_6 ...: \n'); %Walk6_Algorithm_old(nodeCount,clusterCount,hash,C,record,degreeVector)
   [nodeScore_w6,scoreComputationTime_w6] = ...
       Walk6_Algorithm(nodeCount,clusterCount,hash,C,degree);
   scoreComputationTime_w6= hashingTime+scoreComputationTime_w6;
   fprintf('Walk-6 Total Time : %0.2f\n',(scoreComputationTime_w6));
   fprintf('\t*** Computed Walk_6 *** \n');
   
   for k=1:countofRecordedValues
       [eigenDropPercent_walk8,greedyTime_walk8]=greedyPlacement(matrix,...
           nodeCount,k*loopStepSize,nodeScore_w8,largestLam);
        walk8Time(k)=greedyTime_walk8+scoreComputationTime_w8;
        walk8EigenDropPercentage(k)=eigenDropPercent_walk8;
   end
   
   for k=1:countofRecordedValues
       [eigenDropPercent_walk6,greedyTime_walk6]=greedyPlacement(matrix,...
           nodeCount,k*loopStepSize,nodeScore_w6,largestLam);
        walk6Time(k)=greedyTime_walk6+scoreComputationTime_w6;
        walk6EigenDropPercentage(k)=eigenDropPercent_walk6;
   end
   
end

Y=[X,nsEigenDropPercentage,walk6EigenDropPercentage,walk8EigenDropPercentage,...
    nsTime,walk6Time,walk8Time];

fid = fopen(strcat('ResultFiles\',...
    outputFileName,'.csv'),'w');
textHeader='k,ns_EigenDrop,walk6_EigenDrop,walk8_EigenDrop,ns_Time,walk6_time,walk8_time';
fprintf(fid,'%s\n',textHeader);
fclose(fid);
%write data to end of file
dlmwrite(strcat('ResultFiles\',...
    outputFileName,'.csv'),Y,'-append');