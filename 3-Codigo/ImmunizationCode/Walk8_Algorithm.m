function [nodeScore,totalWalk8Time] = Walk8_Algorithm(nodeCount,clusterCount,hash,C,degreeVector)
tic;
totalWalk8Time=0;
nodeScore=zeros(nodeCount,1);

sum_2pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);
sum_3pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
sum_4pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
sum_5pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
sum_6pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  
sum_8pow_deg_of_nodes_in_C_i=zeros(clusterCount,1);  

for i=1:clusterCount
    sum_2pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^2);
    sum_3pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^3);
    sum_4pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^4);
    sum_5pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^5);
    sum_6pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^6);
    sum_8pow_deg_of_nodes_in_C_i(i)=sum(degreeVector(hash==i).^8);
end

sum_2pow_deg_of_nodes_in_C_i=sum_2pow_deg_of_nodes_in_C_i+1;
sum_3pow_deg_of_nodes_in_C_i=sum_3pow_deg_of_nodes_in_C_i+1;
sum_4pow_deg_of_nodes_in_C_i=sum_4pow_deg_of_nodes_in_C_i+1;
sum_5pow_deg_of_nodes_in_C_i=sum_5pow_deg_of_nodes_in_C_i+1;
sum_6pow_deg_of_nodes_in_C_i=sum_6pow_deg_of_nodes_in_C_i+1;
sum_8pow_deg_of_nodes_in_C_i=sum_8pow_deg_of_nodes_in_C_i+1;

C2=C*C;
C3=C2*C;
C4=C2*C2;
C5=C4*C;
C6=C3*C3;
C8=C4*C4;
scoreTerms=zeros(7,1);
for u=1:nodeCount

       scoreTerms(1) = (8*C8(hash(u),hash(u)))*degreeVector(u)^8/sum_8pow_deg_of_nodes_in_C_i(hash(u));      
       scoreTerms(2) = -8*(degreeVector(u))*(C6(hash(u),hash(u))*degreeVector(u)^6/sum_6pow_deg_of_nodes_in_C_i(hash(u)));
       scoreTerms(3) = -8*(C3(hash(u),hash(u))*degreeVector(u)^3/sum_3pow_deg_of_nodes_in_C_i(hash(u)))*...
           (C5(hash(u),hash(u))*degreeVector(u)^5/sum_5pow_deg_of_nodes_in_C_i(hash(u)));
       scoreTerms(4) = -4*(C4(hash(u),hash(u))*degreeVector(u)^4/sum_4pow_deg_of_nodes_in_C_i(hash(u)))^2;
       scoreTerms(5) = 8*(degreeVector(u))*((C3(hash(u),hash(u))*degreeVector(u)^3/sum_3pow_deg_of_nodes_in_C_i(hash(u)))^2);
       scoreTerms(6) = 8*(degreeVector(u)^2)*(C4(hash(u),hash(u))*degreeVector(u)^4/sum_4pow_deg_of_nodes_in_C_i(hash(u)));
       scoreTerms(7) = -2*(C2(hash(u),hash(u))*degreeVector(u)^2/sum_2pow_deg_of_nodes_in_C_i(hash(u)))^4;
       
      nodeScore(u)=scoreTerms(1)+scoreTerms(2)+scoreTerms(3)+scoreTerms(4)+scoreTerms(5)+scoreTerms(6)+scoreTerms(7);
      
end
totalWalk8Time=toc;
fprintf('\t Walk-8 Score Computation Time = %0.2f\n',totalWalk8Time);

end