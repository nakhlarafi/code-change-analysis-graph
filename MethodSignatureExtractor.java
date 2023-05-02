package ca.concordia.soen;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.dom.*;

public class MethodSignatureExtractor {
    public static void main(String[] args) throws IOException {
        int[] folderNumbers = {1, 8, 9};
//        int[] folderNumbers = {14};
        for (int folderNumber : folderNumbers) {
            String folderName = "/Users/tahminaakter/Desktop/ASE23-Bias/Grace/Time/time_" + folderNumber + "_copy";
            File projectDirectory = new File(folderName);
            if (!projectDirectory.isDirectory()) {
                System.err.println("Invalid project path: " + folderName);
                continue;
            }

            FileWriter fileWriter = new FileWriter(folderNumber + ".txt");
            processDirectory(projectDirectory, fileWriter, folderName);
            fileWriter.close();
        }
    }

    private static void processDirectory(File directory, FileWriter fileWriter, String rootFolderName) throws IOException {
        for (File file : directory.listFiles()) {
            if (file.isDirectory()) {
                if (!file.getAbsolutePath().contains(rootFolderName + File.separator + "test")) {
                    processDirectory(file, fileWriter, rootFolderName);
                }
            } else if (file.getName().endsWith(".java")) {
                processJavaFile(file, fileWriter);
            }
        }
    }

    private static void processJavaFile(File file, FileWriter fileWriter) throws IOException {
        String fileContent = new String(java.nio.file.Files.readAllBytes(file.toPath()));
        CompilationUnit cu = parse(fileContent);

        cu.accept(new ASTVisitor() {
            //            public boolean visit(MethodDeclaration node) {
//                IMethodBinding methodBinding = node.resolveBinding();
//                int startLineNumber = cu.getLineNumber(node.getStartPosition());
//                int endLineNumber = cu.getLineNumber(node.getStartPosition() + node.getLength());
//
//                if (methodBinding != null) {
//                    ITypeBinding declaringClass = methodBinding.getDeclaringClass();
//                    String methodSignature = getMethodSignature((ITypeBinding) declaringClass, methodBinding);
//
//                    try {
//                        for (int lineNumber = startLineNumber; lineNumber <= endLineNumber; lineNumber++) {
//                            fileWriter.write(methodSignature + ":" + lineNumber + "\n");
//                        }
//                    } catch (IOException e) {
//                        e.printStackTrace();
//                    }
//                }
//
//                return true;
//            }
//            private String getMethodSignature(ITypeBinding declaringClass, IMethodBinding methodBinding) {
//                StringBuilder signature = new StringBuilder();
//                String binaryName = declaringClass.getBinaryName();
//                if (binaryName != null) {
//                    signature.append(binaryName);
//                } else {
//                    signature.append(declaringClass.getQualifiedName().replace('.', '$'));
//                }
//                signature.append(':').append(methodBinding.getName());
//                signature.append('(');
//
//                ITypeBinding[] parameterTypes = methodBinding.getParameterTypes();
//                for (int i = 0; i < parameterTypes.length; i++) {
//                    if (i > 0) {
//                        signature.append(",");
//                    }
//                    binaryName = parameterTypes[i].getBinaryName();
//                    if (binaryName != null) {
//                        signature.append(binaryName.replace('/', '.'));
//                    } else {
//                        signature.append(parameterTypes[i].getQualifiedName().replace('/', '.'));
//                    }
//                }
//
//                signature.append(')');
//                return signature.toString();
//            }
            public boolean visit(MethodDeclaration node) {
                IMethodBinding methodBinding = node.resolveBinding();
                int startLineNumber = cu.getLineNumber(node.getStartPosition());
                int endLineNumber = cu.getLineNumber(node.getStartPosition() + node.getLength());

                if (methodBinding != null) {
                    IBinding declaringClass = methodBinding.getDeclaringClass();
                    String methodSignature = getMethodSignature(methodBinding);

                    try {
                        for (int lineNumber = startLineNumber; lineNumber <= endLineNumber; lineNumber++) {
                            fileWriter.write(((ITypeBinding) declaringClass).getQualifiedName() + ":" + methodSignature + ":" + lineNumber + "\n");
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }

                return true;
            }
            private String getMethodSignature(IMethodBinding methodBinding) {
                StringBuilder signature = new StringBuilder();
                signature.append(methodBinding.getName());
                signature.append('(');

                ITypeBinding[] parameterTypes = methodBinding.getParameterTypes();
                for (int i = 0; i < parameterTypes.length; i++) {
                    if (i > 0) {
                        signature.append("");
                    }
                    signature.append(getTypeSignature(parameterTypes[i]));
                }

                signature.append(')');
                signature.append(getTypeSignature(methodBinding.getReturnType()));
                return signature.toString();
            }

            private String getTypeSignature(ITypeBinding typeBinding) {
                if (typeBinding.isPrimitive()) {
                    return getPrimitiveTypeCode(typeBinding);
                } else if (typeBinding.isArray()) {
                    return "[" + getTypeSignature(typeBinding.getElementType());
                } else {
                    String binaryName = typeBinding.getBinaryName();
                    if (binaryName == null) {
                        ITypeBinding erasure = typeBinding.getErasure();
                        if (erasure != null) {
                            binaryName = erasure.getBinaryName();
                        }
                    }
                    if (binaryName != null) {
                        return "L" + binaryName.replace('.', '/') + ";";
                    } else {
                        // This should not happen, but we return an empty string just in case
                        return "";
                    }
                }
            }


            private String getPrimitiveTypeCode(ITypeBinding typeBinding) {
                switch (typeBinding.getName()) {
                    case "byte":
                        return "B";
                    case "char":
                        return "C";
                    case "double":
                        return "D";
                    case "float":
                        return "F";
                    case "int":
                        return "I";
                    case "long":
                        return "J";
                    case "short":
                        return "S";
                    case "boolean":
                        return "Z";
                    default:
                        return "";
                }
            }



        });


    }

    private static CompilationUnit parse(String source) {
        ASTParser parser = ASTParser.newParser(AST.JLS15);
        parser.setSource(source.toCharArray());
        parser.setResolveBindings(true);
        parser.setBindingsRecovery(true);
        parser.setCompilerOptions(JavaCore.getOptions());
        parser.setEnvironment(null, null, null, true);
        parser.setUnitName("any_name");

        return (CompilationUnit) parser.createAST(null);
    }
}
