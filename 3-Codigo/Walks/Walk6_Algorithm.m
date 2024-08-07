function [nodeScore,totalWalk6Time] = Walk6_Algorithm(nodeCount,clusterCount,hash,C,degreeVector)
    tic;
    totalWalk6Time=0;
    nodeScore=zeros(nodeCount,1);

    sum_2pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);
    sum_3pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
    sum_4pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
    sum_6pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  

    for i=1:clusterCount
        sum_2pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^2);
        sum_3pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^3);
        sum_4pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^4);
        sum_6pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^6);
    end

    sum_2pow_deg_of_nodes_in_C_i=sum_2pow_deg_of_nodes_in_C_i+1;
    sum_3pow_deg_of_nodes_in_C_i=sum_3pow_deg_of_nodes_in_C_i+1;
    sum_4pow_deg_of_nodes_in_C_i=sum_4pow_deg_of_nodes_in_C_i+1;
    sum_6pow_deg_of_nodes_in_C_i=sum_6pow_deg_of_nodes_in_C_i+1;


    C2=C*C;
    C3=C2*C;
    C4=C2*C2;
    C6=C3*C3;


    scoreTerms=zeros(4,1);
    for u=1:nodeCount

        scoreTerms(1) = 6*C6(hash(u),hash(u))*degreeVector(u)^6/sum_6pow_deg_of_nodes_in_C_i(hash(u));
        scoreTerms(2) = 6*degreeVector(u)*C4(hash(u),hash(u))*degreeVector(u)^4/sum_4pow_deg_of_nodes_in_C_i(hash(u));
        scoreTerms(3) = 3*((C3(hash(u),hash(u))*degreeVector(u)^3/sum_3pow_deg_of_nodes_in_C_i(hash(u)))^2);
        scoreTerms(4) = 2*(degreeVector(u)^3);

        nodeScore(u)=scoreTerms(1)-scoreTerms(2)-scoreTerms(3)+scoreTerms(4); 

    end
    totalWalk6Time=toc;
    fprintf('\t Walk-6 Score Computation Time = %0.2f\n',totalWalk6Time);
end


% for i=1:nodeCount      
%        factor1_f2=( 6*C6(hash(i),hash(i)))*D(i,hash(i))^6/cluster_Degree6(hash(i));
%        factor2_f2=(6 *degreeVector(i)*C4(hash(i),hash(i))*D(i,hash(i))^4/cluster_Degree4(hash(i) ));
%        factor3_f2 = 3*((C3(hash(i),hash(i))*D(i,hash(i))^3/cluster_Degree3(hash(i) ))^2);
%        nodeScore_f2(i)=(2*(degreeVector(i))^3) + factor1_f2 - factor2_f2 - factor3_f2; 
%        if(nodeScore_f2(i)<0)
%            negativeScoreCount=negativeScoreCount+1;
%        end      
% end  









%    cluster_Degree=zeros(clusterCount,1);
%    cluster_Degree3=zeros(clusterCount,1);
%    cluster_Degree4=zeros(clusterCount,1);
%    cluster_Degree6=zeros(clusterCount,1);
%    nodeScore_f2=zeros(nodeCount,1);
%    cluster_Degree=sum(D);
%    length(degreeVector)
   
%    for i=1:clusterCount
%        if(isempty(record{i}))
%            fprintf('in if part...\n')
%            cluster_Degree(i)=1;
%        else
%            fprintf('in else part...\n')
%            cluster_Degree(i)=sum(degreeVector(record{i}))+1;
%        end
%        
%        cluster_Degree(i)=sum(degreeVector(record{i}))+1;
%        cluster_Degree3(i)=0;
%        cluster_Degree4(i)=0;
%        cluster_Degree6(i)=0;
%    end
   
%    for i=1:clusterCount
%        temp=cell2mat(record(i));
%        for j=1:length(temp)
%            cluster_Degree3(i)=cluster_Degree3(i) + degreeVector(temp(j))^3;
%            cluster_Degree4(i)=cluster_Degree4(i) + degreeVector(temp(j))^4;
%            cluster_Degree6(i)=cluster_Degree6(i) + degreeVector(temp(j))^6; 
%        end
%        
%        cluster_Degree3(i)=cluster_Degree3(i) + 1;
%        cluster_Degree4(i)=cluster_Degree4(i) + 1;
%        cluster_Degree6(i)=cluster_Degree6(i) + 1;
%    end

%     for i=1:clusterCount   
% %        temp=cell2mat(record(i));
%        for j=1:nodeCount
%            cluster_Degree3(i)=cluster_Degree3(i) + D(j,i)^3;
%            cluster_Degree4(i)=cluster_Degree4(i) + D(j,i)^4;
%            cluster_Degree6(i)=cluster_Degree6(i) + D(j,i)^6;
%              
%        end
%     end
%    
%        cluster_Degree3=cluster_Degree3 + 1;
%        cluster_Degree4=cluster_Degree4 + 1;
%        cluster_Degree6=cluster_Degree6 + 1;
%        
%    
%    C3=C^3;
%    C4=C^4;
%    C6=C^6;
%    
%    negativeScoreCount=0;
%    for i=1:nodeCount      
%        factor1_f2=( 6*C6(hash(i),hash(i)))*D(i,hash(i))^6/cluster_Degree6(hash(i));
%        factor2_f2=(6 *degreeVector(i)*C4(hash(i),hash(i))*D(i,hash(i))^4/cluster_Degree4(hash(i) ));
%        factor3_f2 = 3*((C3(hash(i),hash(i))*D(i,hash(i))^3/cluster_Degree3(hash(i) ))^2);
%        nodeScore_f2(i)=(2*(degreeVector(i))^3) + factor1_f2 - factor2_f2 - factor3_f2; 
%        if(nodeScore_f2(i)<0)
%            negativeScoreCount=negativeScoreCount+1;
%        end      
%    end  
%    fprintf('Negative Walk-6 Score Count : %d\n',negativeScoreCount);
% end