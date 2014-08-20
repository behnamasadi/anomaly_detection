function distance = GetDistanceBetweenTwoDists(means1, pis1, covs1, means2, pis2, covs2)
    %V11 and K11 
    for i=1:size(means1,1)
      for j=1:size(means1,1)
         cov1= covs1(i,:,:);
         cov2= covs1(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2)); 
         V11(i,j) = det (inv(inv(cov1)+inv(cov2)));
         K11(i,j) = means1(i,:)*inv(cov1)*(means1(i,:)-means1(j,:))'+means1(j,:)*inv(cov2)*(means1(j,:)-means1(i,:))';
      end
    end

    %V12 and K12
    for i=1:size(means1,1)
      for j=1:size(means2,1)
         cov1= covs1(i,:,:);
         cov2= covs2(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2));
         V12(i,j) = det (inv(inv(cov1)+inv(cov2)));
         K12(i,j) = means1(i,:)*inv(cov1)*(means1(i,:)-means2(j,:))'+means2(j,:)*inv(cov2)*(means2(j,:)-means1(i,:))';
      end
    end
    %end

    %V22 and K22
    for i=1:size(means2,1)
      for j=1:size(means2,1)
         cov1= covs2(i,:,:);
         cov2= covs2(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2));
         V22(i,j) = det (inv(inv(cov1)+inv(cov2)));
         K22(i,j) = means2(i,:)*inv(cov1)*(means2(i,:)-means2(j,:))'+means2(j,:)*inv(cov2)*(means2(j,:)-means2(i,:))';
      end
    end
    %end

    %Sum11
    Sum11 = 0;

    for i=1:size(means1,1)
      for j=1:size(means1,1)
         cov1= covs1(i,:,:);
         cov2= covs1(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2));
         Sum11 = Sum11 + pis1(i)*pis1(j)*sqrt(V11(i,j)/(exp(K11(i,j))*det(cov1)*det(cov2)));
      end
    end

    %Sum12
    Sum12 = 0;

    for i=1:size(means1,1)
      for j=1:size(means2,1)
         cov1= covs1(i,:,:);
         cov2= covs2(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2));
         Sum12 = Sum12 + pis1(i)*pis2(j)*sqrt(V12(i,j)/(exp(K12(i,j))*det(cov1)*det(cov2)));
      end
    end

    %Sum22
    Sum22 = 0;

    for i=1:size(means2,1)
      for j=1:size(means2,1)
         cov1= covs2(i,:,:);
         cov2= covs2(j,:,:);
         cov1 = reshape(cov1,size(covs1,2), size(covs1,2));
         cov2 = reshape(cov2,size(covs1,2), size(covs1,2));
         Sum22 = Sum22 + pis2(i)*pis2(j)*sqrt(V22(i,j)/(exp(K22(i,j))*det(cov1)*det(cov2)));
      end
    end

distance = -log(2*Sum12/(Sum11+Sum22));
%distance = 2*Sum12/(Sum11+Sum22);

